import { useLayoutEffect, useState } from 'react';
import { Icon } from '../icons.jsx';
import { highlight } from '../highlight.js';
import { CodePanel, ComplexityChip, CopyButton, ListenButton } from './bits.jsx';

function SourceTag({ isAI, isGuide, t }) {
  if (isAI) {
    return (
      <span className="tag tag-ai">
        <Icon name="sparkles" className="icon-sm" />
        {t('aiAnswerLabel')}
      </span>
    );
  }
  if (isGuide) {
    return (
      <span className="tag">
        <Icon name="book" className="icon-sm" />
        {t('guideLabel')}
      </span>
    );
  }
  return (
    <span className="tag tag-curated">
      <Icon name="badgeCheck" className="icon-sm" />
      {t('curatedLabel')}
    </span>
  );
}

function FollowupEntry({ t, onOpenDrawer }) {
  return (
    <button type="button" className="followup-entry" onClick={() => onOpenDrawer('')}>
      <span className="entry-icon">
        <Icon name="message" />
      </span>
      <span className="entry-text">
        <span className="entry-title">{t('followupEntryTitle')}</span>
        <br />
        <span className="entry-hint">{t('followupEntryHint')}</span>
      </span>
      <Icon name="arrowRight" />
    </button>
  );
}

function AlgorithmResult({
  d,
  t,
  keySet,
  isDesktop,
  playBtn,
  playerState,
  speakBusyId,
  onToggleSpeak,
  onOpenDrawer,
  onAskMethod,
}) {
  const best = d.approaches.find((a) => a.optimal) || d.approaches[0];
  const isAI = d.source === 'llm';

  // Accordion state mirrors syncAccordions(true): on desktop every card
  // is open; on mobile only the best approach starts open. A new result
  // or a viewport change resets to that initial state.
  const initialMap = () => {
    const map = {};
    d.approaches.forEach((a, i) => {
      map[i] = isDesktop ? true : !!a.optimal;
    });
    return map;
  };
  const [openMap, setOpenMap] = useState(initialMap);
  useLayoutEffect(() => {
    setOpenMap(initialMap());
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [d, isDesktop]);

  const toggleCard = (i) => {
    if (isDesktop) return;
    setOpenMap((prev) => ({ ...prev, [i]: !prev[i] }));
  };

  return (
    <>
      <div className="algo-head">
        <h1>{d.name}</h1>
        <div className="algo-meta">
          <span className="tag">{d.category}</span>
          <SourceTag isAI={isAI} t={t} />
          <span className="tag">
            {d.approaches.length} {t('approachCountWord')}
          </span>
        </div>
        <div className="algo-actions">
          {keySet && (
            <ListenButton
              id="result-listen"
              text={d.summary || d.answer || ''}
              t={t}
              playBtn={playBtn}
              playerState={playerState}
              disabled={speakBusyId === 'result-listen'}
              onToggle={onToggleSpeak}
            />
          )}
          <button type="button" className="btn btn-secondary" onClick={() => onOpenDrawer('')}>
            <Icon name="message" className="icon-sm" />
            <span>{t('askButton')}</span>
          </button>
        </div>
      </div>

      <section className="section-block" aria-labelledby="keyLogicLabel">
        <h2 className="section-label" id="keyLogicLabel">
          {t('keyLogicTitle')}
        </h2>
        <p className="key-logic">{d.key_logic}</p>
      </section>

      <section className="section-block key-code-wrap" aria-labelledby="keyCodeLabel">
        <h2 className="section-label" id="keyCodeLabel">
          {t('keyCodeTitle')}
        </h2>
        <div className="best-ribbon">
          <span className="best-badge">
            <Icon name="check" className="icon-sm" />
            {t('bestBadge')}
          </span>
          <span className="best-note">{best.name}</span>
        </div>
        <div className="code-panel">
          <div className="code-panel-head">
            <span className="approach-name">{best.name}</span>
            <span className="spacer"></span>
            <ComplexityChip label={t('timeLabel')} value={best.time} />
            <ComplexityChip label={t('spaceLabel')} value={best.space} />
            <CopyButton text={best.code} label={t('copyCodeButton')} copiedLabel={t('copiedLabel')} />
          </div>
          <pre>
            <code dangerouslySetInnerHTML={{ __html: highlight(best.code) }} />
          </pre>
        </div>
      </section>

      <section className="section-block" aria-labelledby="approachesLabel">
        <h2 className="section-label" id="approachesLabel">
          {t('approachesTitle')}
        </h2>
        {d.approaches.map((a, i) => {
          const isBest = !!a.optimal;
          const isOpen = isDesktop ? true : !!openMap[i];
          return (
            <article
              key={a.name}
              className={'approach-card' + (isBest ? ' is-best' : '')}
              id={`approach-${i}`}
              data-approach={a.name}
            >
              <div className="approach-head">
                <div className="head-main">
                  <h3>{a.name}</h3>
                  {isBest && (
                    <span className="best-badge">
                      <Icon name="check" className="icon-sm" />
                      {t('bestBadge')}
                    </span>
                  )}
                </div>
                <button
                  type="button"
                  className="approach-toggle"
                  aria-expanded={isOpen ? 'true' : 'false'}
                  aria-controls={`approach-body-${i}`}
                  aria-label={a.name}
                  onClick={() => toggleCard(i)}
                >
                  <Icon name="chevronDown" />
                </button>
              </div>
              <div className="approach-body" id={`approach-body-${i}`} hidden={!isOpen}>
                <p className="approach-logic">{a.logic}</p>
                <div className="approach-meta">
                  <ComplexityChip label={t('timeLabel')} value={a.time} />
                  <ComplexityChip label={t('spaceLabel')} value={a.space} />
                </div>
                <CodePanel title="Java" code={a.code} copyLabel={t('copyCodeButton')} copiedLabel={t('copiedLabel')} />
                <div className="approach-actions">
                  <button
                    type="button"
                    className="btn btn-secondary btn-sm"
                    onClick={() => onAskMethod(a.name)}
                  >
                    <Icon name="message" className="icon-sm" />
                    <span>{t('askAboutButton')}</span>
                  </button>
                </div>
              </div>
            </article>
          );
        })}
      </section>

      <FollowupEntry t={t} onOpenDrawer={onOpenDrawer} />
    </>
  );
}

function PlainAnswerResult({
  d,
  t,
  keySet,
  playBtn,
  playerState,
  speakBusyId,
  onToggleSpeak,
  onOpenDrawer,
  onSuggestSearch,
}) {
  const isGuide = !d.matched && !!d.family;
  const isAI = d.source === 'llm';
  return (
    <>
      <div className="algo-head">
        <h1>{d.topic || d.category || ''}</h1>
        <div className="algo-meta">
          <span className="tag">{d.category || ''}</span>
          <SourceTag isAI={isAI} isGuide={isGuide} t={t} />
        </div>
        <div className="algo-actions">
          {keySet && (
            <ListenButton
              id="result-listen"
              text={d.summary || d.answer || ''}
              t={t}
              playBtn={playBtn}
              playerState={playerState}
              disabled={speakBusyId === 'result-listen'}
              onToggle={onToggleSpeak}
            />
          )}
          <button type="button" className="btn btn-secondary" onClick={() => onOpenDrawer('')}>
            <Icon name="message" className="icon-sm" />
            <span>{t('askButton')}</span>
          </button>
        </div>
      </div>
      <div className="answer-panel">
        <p className="answer-text">{d.answer || ''}</p>
        {d.suggestions && d.suggestions.length > 0 && (
          <div className="guide-suggest">
            {d.suggestions.map((s) => (
              <button key={s} type="button" className="chip" onClick={() => onSuggestSearch(s)}>
                {s}
              </button>
            ))}
          </div>
        )}
        <div className="answer-actions">
          <CopyButton
            text={d.answer || ''}
            label={t('copyButton')}
            copiedLabel={t('copiedLabel')}
            className="btn btn-ghost btn-sm"
          />
        </div>
      </div>
      <div style={{ height: '24px' }}></div>
      <FollowupEntry t={t} onOpenDrawer={onOpenDrawer} />
    </>
  );
}

export function LoadingSkeleton({ t }) {
  return (
    <div className="loading-block" role="status" aria-label={t('thinking')}>
      <div className="skeleton" style={{ height: '38px', width: '55%' }}></div>
      <div className="skeleton" style={{ height: '20px', width: '85%' }}></div>
      <div className="skeleton" style={{ height: '20px', width: '70%' }}></div>
      <div className="skeleton" style={{ height: '180px' }}></div>
      <div className="skeleton" style={{ height: '140px' }}></div>
    </div>
  );
}

export default function ResultView(props) {
  const { data, loading } = props;
  return (
    <article id="resultArticle" className="result-article" aria-busy={loading ? 'true' : 'false'}>
      {loading ? (
        <LoadingSkeleton t={props.t} />
      ) : data ? (
        data.kind === 'algorithm' ? (
          <AlgorithmResult {...props} d={data} />
        ) : (
          <PlainAnswerResult {...props} d={data} />
        )
      ) : null}
    </article>
  );
}

export function ApproachNav({ approaches, activeId, t, onNavigate }) {
  const list = approaches && approaches.length ? approaches : [];
  return (
    <nav id="approachNav" className="approach-nav" aria-label="Approaches" hidden={list.length === 0}>
      <p className="nav-label">{t('approachesTitle')}</p>
      <ul className="nav-list" id="navList">
        {list.map((a, i) => (
          <li key={a.name}>
            <button
              type="button"
              className={'nav-item' + (activeId === `approach-${i}` ? ' active' : '')}
              data-target={`approach-${i}`}
              onClick={() => onNavigate(`approach-${i}`)}
            >
              {a.optimal && <span className="dot-best" aria-hidden="true"></span>}
              <span>{a.name}</span>
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );
}
