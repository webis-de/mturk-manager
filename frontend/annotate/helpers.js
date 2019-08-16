import _ from 'lodash';
import Loader from './loader';

function normalize_answer(answer_raw) {
  const answer = {};
  if (Array.isArray(answer_raw.QuestionFormAnswers.Answer)) {
    _.forEach(answer_raw.QuestionFormAnswers.Answer, (value) => {
      answer[value.QuestionIdentifier] = value.FreeText;
    });
  } else {
    answer[answer_raw.QuestionFormAnswers.Answer.QuestionIdentifier] = answer_raw.QuestionFormAnswers.Answer.FreeText;
  }

  return answer;
}

function add_to_object_assignments_selected(
  loader,
  id_assignment,
  state,
  message,
) {
  loader.object_assignments_selected[id_assignment] = {
    state,
    message,
  };

  $(`button[data-id_assignment="${id_assignment}"]`).removeClass('active');
}

export { normalize_answer, add_to_object_assignments_selected };