// Learning Orb SVG — orbSVG() extracted VERBATIM from
// templates/index.html of the Flask build. The `p` prefix keeps the
// gradient IDs unique between the home orb and the voice-sheet orb.

function orbSVG(p) {
  return '<svg viewBox="0 0 160 160" role="img" aria-label="">'
    + '<defs>'
    + '<radialGradient id="' + p + 'Core" cx="38%" cy="32%" r="78%"><stop offset="0%" stop-color="#C4B9FF"/><stop offset="45%" stop-color="#8B7CFF"/><stop offset="100%" stop-color="#4B3DB8"/></radialGradient>'
    + '<radialGradient id="' + p + 'Glow" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#8B7CFF" stop-opacity=".35"/><stop offset="100%" stop-color="#8B7CFF" stop-opacity="0"/></radialGradient>'
    + '</defs>'
    + '<circle cx="80" cy="80" r="76" fill="url(#' + p + 'Glow)"/>'
    + '<circle class="orb-ring r1" cx="80" cy="80" r="58" fill="none" stroke="#8B7CFF" stroke-width="1.5"/>'
    + '<circle class="orb-ring r2" cx="80" cy="80" r="58" fill="none" stroke="#FFB86B" stroke-width="1.5"/>'
    + '<circle class="orb-ring r3" cx="80" cy="80" r="58" fill="none" stroke="#43D9C3" stroke-width="1.5"/>'
    + '<g class="orb-dot d1"><circle cx="80" cy="18" r="4" fill="#FFB86B"/></g>'
    + '<g class="orb-dot d2"><circle cx="80" cy="18" r="3" fill="#43D9C3"/></g>'
    + '<g class="orb-dot d3"><circle cx="80" cy="18" r="2.5" fill="#B7AFFF"/></g>'
    + '<g class="orb-core"><circle cx="80" cy="80" r="46" fill="url(#' + p + 'Core)"/>'
    + '<ellipse cx="64" cy="60" rx="18" ry="11" fill="#fff" opacity=".18"/>'
    + '<rect x="62" y="68" width="7" height="24" rx="3.5" fill="#fff" opacity=".85"/>'
    + '<rect x="76.5" y="58" width="7" height="44" rx="3.5" fill="#fff"/>'
    + '<rect x="91" y="68" width="7" height="24" rx="3.5" fill="#fff" opacity=".85"/>'
    + '<circle class="orb-spark" cx="104" cy="52" r="3" fill="#fff"/>'
    + '<circle class="orb-spark" cx="52" cy="100" r="2.4" fill="#fff"/></g>'
    + '</svg>';
}

export function Orb({ prefix, state, id, className, orbRef }) {
  return (
    <div
      ref={orbRef}
      id={id}
      className={className}
      data-orb-state={state}
      aria-hidden="true"
      dangerouslySetInnerHTML={{ __html: orbSVG(prefix) }}
    />
  );
}
