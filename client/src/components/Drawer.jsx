import { Icon } from '../icons.jsx';
import { CopyButton, ListenButton } from './bits.jsx';

// Conversation drawer (desktop panel / mobile bottom sheet) — port of
// the drawer logic in the original page: explicit context, level chip,
// suggested questions, Q&A thread with Listen/Copy per answer.
export default function Drawer({
  mounted,
  open,
  algorithmName,
  focus,
  approaches,
  exchanges,
  t,
  keySet,
  playBtn,
  playerState,
  speakBusyId,
  onClose,
  onSendFollowup,
  onMic,
  onToggleSpeak,
  inputRef,
  threadRef,
}) {
  if (!mounted) return null;

  const best = (approaches || []).find((a) => a.optimal);
  const suggested = [];
  if (best) suggested.push(t('suggWhyBest').replace('{approach}', best.name));
  suggested.push(t('suggComplexity'), t('suggExample'), t('suggSimpler'));

  const handleSubmit = (e) => {
    e.preventDefault();
    onSendFollowup(inputRef.current ? inputRef.current.value : '');
  };

  return (
    <>
      {open && <div id="drawerScrim" className="scrim desktop-none" onClick={onClose}></div>}
      <aside
        id="drawer"
        className={'drawer' + (open ? ' open' : '')}
        role="dialog"
        aria-modal="false"
        aria-labelledby="drawerTitle"
      >
        <div className="drawer-head">
          <div className="head-text">
            <p className="drawer-context" id="drawerContext">
              {algorithmName}
              {focus && (
                <>
                  {' '}
                  <span className="ctx-arrow" aria-hidden="true">
                    →
                  </span>{' '}
                  {focus}
                </>
              )}
            </p>
            <h2 id="drawerTitle">{t('drawerTitle')}</h2>
          </div>
          <button
            type="button"
            id="drawerClose"
            className="icon-btn"
            aria-label={t('closeButton')}
            onClick={onClose}
          >
            <Icon name="x" />
          </button>
        </div>
        <div className="level-row" id="drawerLevel">
          {focus ? (
            <span className="level-chip method">
              {t('aboutMethodChip')}: {focus}
            </span>
          ) : (
            <span className="level-chip">{t('aboutAlgorithmChip')}</span>
          )}
        </div>
        <div id="qaThread" className="qa-thread" aria-live="polite" ref={threadRef}>
          {exchanges.length === 0 ? (
            <p className="thread-empty">{t('drawerEmpty')}</p>
          ) : (
            exchanges.map((ex) => (
              <div key={ex.id} style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <span className="level-chip" style={{ alignSelf: 'flex-start' }}>
                  {ex.levelText}
                </span>
                <div className="bubble-q">{ex.question}</div>
                <div className="bubble-a">
                  <p className="answer-text" aria-live="polite">
                    {ex.answer}
                  </p>
                  <div className="bubble-meta">
                    {ex.data && ex.data.llm && (
                      <span className="tag tag-ai">
                        <Icon name="sparkles" className="icon-sm" />
                        {t('aiAnswerLabel')}
                      </span>
                    )}
                    {keySet && ex.data && (
                      <ListenButton
                        id={`ex-${ex.id}-listen`}
                        text={ex.data.answer || ''}
                        t={t}
                        playBtn={playBtn}
                        playerState={playerState}
                        disabled={speakBusyId === `ex-${ex.id}-listen`}
                        onToggle={onToggleSpeak}
                        className="mini-btn"
                      />
                    )}
                    {ex.data && (
                      <CopyButton
                        text={ex.data.answer || ''}
                        label={t('copyButton')}
                        copiedLabel={t('copiedLabel')}
                        className="mini-btn"
                      />
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
        <div className="drawer-suggest" id="drawerSuggest">
          <span className="sr-only">{t('suggestedTitle')}: </span>
          {suggested.map((q) => (
            <button key={q} type="button" className="chip" onClick={() => onSendFollowup(q)}>
              {q}
            </button>
          ))}
        </div>
        <form id="drawerForm" className="drawer-form" autoComplete="off" onSubmit={handleSubmit}>
          <label className="sr-only" htmlFor="drawerInput">
            {t('followupPlaceholder')}
          </label>
          <input
            ref={inputRef}
            id="drawerInput"
            type="text"
            enterKeyHint="send"
            placeholder={t('followupPlaceholder')}
          />
          <button
            type="button"
            id="drawerMicBtn"
            className="mic-btn"
            aria-label={t('micStart')}
            onClick={onMic}
          >
            <Icon name="mic" />
          </button>
          <button
            type="submit"
            id="drawerSendBtn"
            className="send-btn"
            aria-label={t('sendButton')}
          >
            <Icon name="send" />
          </button>
        </form>
      </aside>
    </>
  );
}
