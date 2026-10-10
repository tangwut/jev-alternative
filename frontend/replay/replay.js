(function () {
  'use strict';
  const data = window.LayaRecordings;
  const get = id => document.getElementById(id);
  let timer;
  let stage = 0;

  function current() { return data.records.find(record => record.id === get('scenario').value); }

  function render() {
    const record = current();
    const [questionId, question] = Object.entries(record.request.questions).find(([, q]) => q.type === 'choice');
    const answer = record.response.answers[questionId];
    const choice = answer.choice;
    get('state').textContent = record.request.state.message;
    get('request').textContent = JSON.stringify(record.request, null, 2);
    get('response').textContent = JSON.stringify(record.response, null, 2);
    get('candidates').replaceChildren();
    for (const [label, description] of Object.entries(question.criteria)) {
      const item = document.createElement('div');
      item.className = 'option' + (stage === 3 && label === choice ? ' selected' : '');
      const text = document.createElement('div');
      const title = document.createElement('strong');
      title.textContent = label;
      const caption = document.createElement('small');
      caption.textContent = description;
      text.append(title, caption);
      const probability = document.createElement('span');
      probability.className = 'percent';
      const value = answer.probabilities?.[label];
      probability.textContent = stage === 3 && typeof value === 'number' ? `${(value * 100).toFixed(1)}%` : '—';
      item.append(text, probability);
      get('candidates').append(item);
    }
    for (let i = 1; i <= 3; i++) get(`step${i}`).className = 'step' + (i <= stage ? ' active' : '');
    get('decision').textContent = stage === 3 ? choice : ['Ready to replay', 'Reading the state…', 'Comparing candidates…'][stage];
    get('detail').textContent = stage === 3 ? 'Recorded model choice. Candidate probabilities are not a measure of task accuracy.' : 'Press replay to walk through the recorded decision.';
    get('metadata').textContent = `Recorded ${data.metadata.recorded_on} · ${record.response.routing.model} · ${data.metadata.device} · ${data.metadata.platform}. Single recorded request: ${record.elapsed_ms} ms; not a benchmark.`;
  }

  function tick() {
    stage++;
    render();
    if (stage < 3) timer = setTimeout(tick, 650);
    else get('replay').disabled = false;
  }

  get('replay').onclick = () => {
    clearTimeout(timer);
    stage = 0;
    get('replay').disabled = true;
    tick();
  };
  get('scenario').onchange = () => {
    clearTimeout(timer);
    stage = 0;
    get('replay').disabled = false;
    render();
  };
  render();
})();
