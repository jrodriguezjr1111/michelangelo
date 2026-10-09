// ============================================================================
// Reticle Delta — CyberWing corporate mark as native OpenSCAD geometry.
// Transcribed from canary/media/images/brand/cyberwing-logo/
// cyberwing-g-mark-transparent.svg (viewBox 200, centre 100,100):
//   ring  r = 78, stroke 14  -> 71..85; twelve 30 deg sectors, eleven carry a
//         segment (~4..26 deg of each sector), the NE sector carries a DOT r=8
//   delta apex (100,44), wing tips (52,142)/(148,142), notch (100,128),
//         tail (100,160)  -> four facets
// SVG y is DOWN; here y is UP.  Unit = SVG px; scale with `s` (mark Ø = 170 px).
// 2D modules only — extrude at the call site (emboss / inlay pocket / plate).
// ============================================================================
function _pt(x, y) = [x - 100, 100 - y];

module mark_ring(seg_gap = 8) {
  // eleven segments + the dot sector (index 10 counting CCW from +X is NE=45deg)
  for (k = [0:11]) {
    a0 = k * 30 + seg_gap / 2; a1 = (k + 1) * 30 - seg_gap / 2;
    if (k != 1)                                   // sector 30..60 deg = NE = the dot
      polygon(concat(
        [for (a = [a0:(a1 - a0) / 6:a1 + 0.01]) 85 * [cos(a), sin(a)]],
        [for (a = [a1:-(a1 - a0) / 6:a0 - 0.01]) 71 * [cos(a), sin(a)]]));
  }
  translate(78 * [cos(45), sin(45)]) circle(r = 8, $fn = 24);
}

module mark_delta(facet = 0) {
  // facet 0 = whole silhouette; 1..4 = the four facets (for two-level emboss)
  A = _pt(100, 44); L = _pt(52, 142); R = _pt(148, 142);
  N = _pt(100, 128); T = _pt(100, 160);
  if (facet == 0) polygon([A, L, T, R]);          // outer silhouette (N is interior)
  if (facet == 1) polygon([A, L, N]);
  if (facet == 2) polygon([A, N, R]);
  if (facet == 3) polygon([L, N, T]);
  if (facet == 4) polygon([N, R, T]);
}

module mark2d() { mark_ring(); mark_delta(0); }

// raised mark, two facet heights so the delta reads faceted under raking light
module mark3d(d = 40, h = 1.2) {
  s = d / 170;
  scale([s, s, 1]) {
    linear_extrude(h) mark_ring();
    linear_extrude(h) { mark_delta(1); mark_delta(4); }
    linear_extrude(h * 0.5) { mark_delta(2); mark_delta(3); }
  }
}
