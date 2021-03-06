'''
Look at error rates only scoring utterances that contain OOVs
'''

OOV_FILE = '/deep/u/zxie/ctc_clm_transcripts/oovs.txt'

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('hyp')
    parser.add_argument('stm')
    parser.add_argument('hyp_out')
    parser.add_argument('stm_out')
    args = parser.parse_args()

    # Read in utt keys with OOVs
    oov_utts = set()
    with open(OOV_FILE, 'r') as fin:
        lines = fin.read().strip().splitlines()
    for l in lines:
        utt_key, oov_word = l.split(' ', 1)
        oov_utts.add(utt_key)

    # Read in hyps
    with open(args.hyp, 'r') as fin:
        lines = fin.read().strip().splitlines()

    # Write the filtered hyp file
    oov_utt_count = 0
    tot_utt_count = 0
    fout = open(args.hyp_out, 'w')
    for l in lines:
        parts = l.split(' ', 1)
        if len(parts) == 1:
            tot_utt_count += 1
            continue
        utt_key, utt = parts
        if utt_key not in oov_utts:
            tot_utt_count += 1
            continue
        fout.write(l + '\n')
        tot_utt_count += 1
        oov_utt_count += 1
    fout.close()
    # Sanity check
    print '%d/%d utts contain oovs' % (oov_utt_count, tot_utt_count)

    # Read in stm reference file
    stm_oov_utts = 0
    oov_utt_starts = set()
    for ou in oov_utts:
        ou_start = '-'.join(ou.split('-')[0:2])
        oov_utt_starts.add(ou_start)
    with open(args.stm, 'r') as fin:
        lines = fin.read().strip().splitlines()
    fout = open(args.stm_out, 'w')
    for l in lines:
        # Handle comments
        if l.startswith(';;'):
            fout.write(l+'\n')
            continue
        parts = l.split(' ', 6)
        utt_key_part, channel, utt_key, t_start, t_end, metadata, utt = parts
        stm_utt_key = '%s-%s_%06d' % (utt_key_part, channel.lower(), int(float(t_start) * 100))
        print stm_utt_key
        if stm_utt_key not in oov_utt_starts:
            continue
        fout.write(l + '\n')
        stm_oov_utts += 1
    fout.close()
    # Sanity check
    print '%d/%d stm utts contain oovs' % (stm_oov_utts, tot_utt_count)
