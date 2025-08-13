import re
import pandas as pd
import matplotlib.pyplot as plt

def normalise_id(seq_id):
    if re.search(r'-p\d+$', seq_id):
        base = re.sub(r'-p\d+$', '', seq_id)
        return f"{base}-00001"
    return seq_id

def parse_log_for_data(log_path):
    failed_ids = set()
    success_ids = set()
    timings = {}
    seq_lengths = {}

    re_finish = re.compile(r'Finished prediction in\s+([0-9.]+)\s+seconds', re.IGNORECASE)
    re_residues = re.compile(r'(\d+)\s+residues in this chain', re.IGNORECASE)
    re_save = re.compile(r'Saving prediction to\s+(?:\S*/)?([^/\s]+)\.pdb', re.IGNORECASE)
    re_fail = re.compile(r'Failed to generate\s+(?:\S*/)?([^/\s]+)\.pdb', re.IGNORECASE)

    pending_time = None
    pending_len = None

    with open(log_path, 'r') as f:
        for line in f:
            m_len = re_residues.search(line)
            if m_len:
                pending_len = int(m_len.group(1))
                continue

            m_fail = re_fail.search(line)
            if m_fail:
                fid = normalise_id(m_fail.group(1))
                failed_ids.add(fid)
                timings[fid] = "FAILED"
                seq_lengths[fid] = pending_len
                pending_time = None
                pending_len = None
                continue

            m_fin = re_finish.search(line)
            if m_fin:
                pending_time = float(m_fin.group(1))
                continue

            m_save = re_save.search(line)
            if m_save:
                sid = normalise_id(m_save.group(1))
                success_ids.add(sid)
                if pending_time is not None:
                    timings[sid] = pending_time
                if pending_len is not None:
                    seq_lengths[sid] = pending_len
                pending_time = None
                pending_len = None
                continue

    return failed_ids, success_ids, timings, seq_lengths

def build_df_with_two_logs(failed_before, success_before, timings_before, lengths_before,
                           failed_after, success_after, timings_after, lengths_after):
    all_ids = set().union(failed_before, success_before, failed_after, success_after)

    rows = []
    for seq_id in sorted(all_ids):
        if seq_id in failed_before:
            status_before = "failed"
            time_before = "FAILED"
        elif seq_id in success_before:
            status_before = "success"
            time_before = timings_before.get(seq_id)
        else:
            status_before = "unknown"
            time_before = None

        if seq_id in failed_after:
            status_after = "failed"
            time_after = "FAILED"
        elif seq_id in success_after:
            status_after = "success"
            time_after = timings_after.get(seq_id)
        else:
            status_after = "unknown"
            time_after = None

        rows.append({
            "identifier": seq_id,
            "before_seq_length": lengths_before.get(seq_id),
            "status_before": status_before,
            "timing_before_seconds": time_before,
            "after_seq_length": lengths_after.get(seq_id),
            "status_after": status_after,
            "timing_after_seconds": time_after
        })

    return pd.DataFrame(rows)

def plot_scatter(df, output_png):
    plt.figure(figsize=(10, 6))

    before_mask = pd.to_numeric(df["timing_before_seconds"], errors="coerce").notna()
    after_mask = pd.to_numeric(df["timing_after_seconds"], errors="coerce").notna()

    plt.scatter(
        df.loc[before_mask, "before_seq_length"],
        df.loc[before_mask, "timing_before_seconds"],
        color="blue", alpha=0.6, label="Before"
    )

    plt.scatter(
        df.loc[after_mask, "after_seq_length"],
        df.loc[after_mask, "timing_after_seconds"],
        color="orange", alpha=0.6, label="After"
    )

    plt.xlabel("Sequence Length")
    plt.ylabel("Time (seconds)")
    plt.title("Prediction Time vs Sequence Length")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(output_png, dpi=300)
    plt.close()

# ==== Main execution ====
log_before = "nohup.txt"
log_after = "nohup2.txt"

failed_b, success_b, timings_b, lengths_b = parse_log_for_data(log_before)
failed_a, success_a, timings_a, lengths_a = parse_log_for_data(log_after)

df_all = build_df_with_two_logs(failed_b, success_b, timings_b, lengths_b,
                                failed_a, success_a, timings_a, lengths_a)


print(df_all)
plot_scatter(df_all, "timing_vs_length.png")

