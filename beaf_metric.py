import json
import argparse

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)
    
def answer_check(beaf_qna, model_answers):
    orig_pairs = {}
    for (q, a) in zip(beaf_qna, model_answers):
        assert q['id'] == a['id']
        if 'yes' in a['answer'].lower():
            answer = 'yes'
        elif 'no' in a['answer'].lower():
            answer = 'no'
        
        gt = q['gt']
        
        if gt =='yes' and answer == 'yes':
            q['answer'] = 'TP'
        elif gt == 'no' and answer == 'no':
            q['answer'] = 'TN'
        elif gt == 'yes' and answer == 'no':
            q['answer'] = 'FN'
        elif gt == 'no' and answer == 'yes':
            q['answer'] = 'FP'

        if q['orig_img']:
            if orig_pairs.get(q['image']) is None:
                orig_pairs[q['image']] = {}
            orig_pairs[q['image']][q['question']] = q['answer']
        
        total_qna = beaf_qna.copy()
    return orig_pairs, total_qna

def metric(orig_pairs, total_qna):
    cnt = {'TP':0, 'FP':0, 'TN':0, 'FN':0,
        'TU':0, 'IG':0, 'SBp':0, 'SBn':0, 'ID':0}
    conv = {'TPTN': 'TU', 'FNFP': 'IG', 'TPFP': 'SBp', 'FNTN': 'SBn'}

    id_tot = 0
    for tot in total_qna:
        cnt[tot['answer']] += 1
        if not tot['orig_img']:
            name = tot['image'][:-7] + '.jpg'
            ori_ans = orig_pairs[name][tot['question']]
            # for TU, IG, SBp, SB,n
            if tot['removed_q']:
                if conv.get(ori_ans + tot['answer']) is not None:
                    key = conv[ori_ans + tot['answer']]
                    cnt[key] += 1
            # for ID
            else:
                id_tot += 1
                if ori_ans[0] != tot['answer'][0]:
                    cnt['ID'] += 1

    assert cnt['TP'] + cnt['FP'] + cnt['TN'] + cnt['FN'] == 26118
    assert cnt['TU'] + cnt['IG'] + cnt['SBp'] + cnt['SBn'] == 1727
    
    acc = (cnt['TP'] + cnt['TN']) / (cnt['TP'] + cnt['FP'] + cnt['TN'] + cnt['FN']) * 100
    precision = cnt['TP'] / (cnt['TP'] + cnt['FP']) * 100
    recall = cnt['TP'] / (cnt['TP'] + cnt['FN']) * 100
    f1 = 2 * precision * recall / (precision + recall)

    tu = cnt['TU'] / 1727 * 100
    ig = cnt['IG'] / 1727 * 100
    sbp = cnt['SBp'] / 1727 * 100
    sbn = cnt['SBn'] / 1727 * 100
    id_ = cnt['ID'] / id_tot * 100
    f1_tuid = 2*tu*(100-id_) / (tu + (100-id_))
    return acc, precision, recall, f1, tu, ig, sbp, sbn, id_, f1_tuid

def evaluate(args):
    beaf_qna = load_json(f'{args.qna_path}')
    model_answers = load_json(f'{args.model_answers}')
    orig_pairs, total_qna = answer_check(beaf_qna, model_answers)
    ACC, Precision, Recall, F1_PR, TU, IG, SBp, SBn, ID, F1_TUID = metric(orig_pairs, total_qna)

    print("========================================================")
    print("   Accuracy  |  Precision  |    Recall   |    F1(P,R) ")
    print("--------------------------------------------------------")
    print(f"    {ACC:.2f}    |    {Precision:.2f}    |    {Recall:.2f}    |    {F1_PR:.2f}")
    print("=========================================================")
    print("   TU   |   IG   |   SB+  |   SB-  |   ID   | F1(TU,ID)")
    print("---------------------------------------------------------")
    print(f" {TU:.2f}  |  {IG:.2f}  |  {SBp:.2f} |  {SBn:.2f} |  {ID:.2f}  |   {F1_TUID:.2f}")
    print("=========================================================")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--qna-path", type=str, default="./beaf_qna.json")
    parser.add_argument("--model-answers", type=str, default="./answer_gpt4o.json")
    args = parser.parse_args()

    evaluate(args)


