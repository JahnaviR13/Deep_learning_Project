import json


# def get_QAE(data, text_evidence_only=True):
#     qae = {}
#     data_id = 0
#     for paper_id, paper_data in data.items():
#         for qa_info in paper_data["qas"]:
#             question_id = qa_info["question_id"]
#             question = qa_info["question"]
#             references = []
#             for annotation_info in qa_info["answers"]:
#                 answer_info = annotation_info["answer"]
#                 if answer_info["unanswerable"]:
#                     references.append(
#                         {
#                             "data_id": data_id,
#                             "paper_id": paper_id,
#                             "question": question,
#                             "answer": "Unanswerable",
#                             "evidence": [],
#                             "type": "none",
#                         }
#                     )
#                     data_id += 1
#                 else:
#                     if answer_info["extractive_spans"]:
#                         answer = ", ".join(answer_info["extractive_spans"])
#                         answer_type = "extractive"
#                     elif answer_info["free_form_answer"]:
#                         answer = answer_info["free_form_answer"]
#                         answer_type = "abstractive"
#                     elif answer_info["yes_no"]:
#                         answer = "Yes"
#                         answer_type = "boolean"
#                     elif answer_info["yes_no"] is not None:
#                         answer = "No"
#                         answer_type = "boolean"
#                     else:
#                         raise RuntimeError(
#                             f"Annotation {answer_info['annotation_id']} does"
#                             " not contain an answer"
#                         )
#                     if text_evidence_only:
#                         evidence = [
#                             text
#                             for text in answer_info["evidence"]
#                             if "FLOAT SELECTED" not in text
#                         ]
#                     else:
#                         evidence = answer_info["evidence"]
#                     references.append(
#                         {
#                             "data_id": data_id,
#                             "paper_id": paper_id,
#                             "question": question,
#                             "answer": answer,
#                             "evidence": evidence,
#                             "type": answer_type,
#                         }
#                     )
#                     data_id += 1
#             qae[question_id] = references

#     return qae


def get_QAE2(data, text_evidence_only=True):
    qae = []
    data_id = 0
    for paper_id, paper_data in data.items():
        for qa_info in paper_data["qas"]:
            question = qa_info["question"]
            for annotation_info in qa_info["answers"]:
                answer_info = annotation_info["answer"]
                if answer_info["unanswerable"]:
                    qae.append(
                        {
                            "data_id": data_id,
                            "paper_id": paper_id,
                            "question": question,
                            "answer": "Unanswerable",
                            "evidence": [],
                            "type": "none",
                        }
                    )
                    data_id += 1
                else:
                    if answer_info["extractive_spans"]:
                        answer = ", ".join(answer_info["extractive_spans"])
                        answer_type = "extractive"
                    elif answer_info["free_form_answer"]:
                        answer = answer_info["free_form_answer"]
                        answer_type = "abstractive"
                    elif answer_info["yes_no"]:
                        answer = "Yes"
                        answer_type = "boolean"
                    elif answer_info["yes_no"] is not None:
                        answer = "No"
                        answer_type = "boolean"
                    else:
                        raise RuntimeError(
                            f"Annotation {answer_info['annotation_id']} does"
                            " not contain an answer"
                        )
                    if text_evidence_only:
                        evidence = [
                            text
                            for text in answer_info["evidence"]
                            if "FLOAT SELECTED" not in text
                        ]
                        evidence = " ".join(evidence[:2])
                    else:
                        evidence = " ".join(answer_info["evidence"][:2])
                    qae.append(
                        {
                            "data_id": data_id,
                            "paper_id": paper_id,
                            "question": question,
                            "answer": answer,
                            "evidence": evidence,
                            "type": answer_type,
                        }
                    )
                    data_id += 1
    return qae


def get_all_paragraphs(data):
    all_paragraphs = []
    for paper_id, paper_data in data.items():
        full_text = paper_data["full_text"]
        for section in full_text:
            for paragraph in section["paragraphs"]:
                if len(paragraph.split()) > 10:
                    all_paragraphs.append(
                        {"paper_id": paper_id, "paragraph": paragraph}
                    )
    return all_paragraphs


def save_question_context(input_data, filepath):
    question_context = []
    for qid in input_data:
        data = input_data[qid][0]
        question_context.extend(
            [
                {
                    "pid": data["paper_id"],
                    "question": data["question"],
                    "context": context,
                }
                for context in data["evidence"]
            ]
        )
    qc_json = json.dumps(question_context, indent=2)
    with open(filepath, "w") as outfile:
        outfile.write(qc_json)


def get_all_questions(data):
    questions = []
    for paper_id, paper_data in data.items():
        for qa_info in paper_data["qas"]:
            question_id = qa_info["question_id"]
            question = qa_info["question"]
            questions.append(
                {
                    "paper_id": paper_id,
                    "question_id": question_id,
                    "question": question,
                }
            )
    return questions
