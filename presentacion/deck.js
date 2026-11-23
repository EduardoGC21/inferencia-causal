for (const element of document.querySelectorAll('[data-tex]')) {
  katex.render(element.dataset.tex, element, {
    displayMode: element.classList.contains('equation'),
    throwOnError: true
  });
}

{
  const art = document.querySelector('.cover-art');
  const ctx = art.getContext('2d');
  ctx.scale(art.width / 390, art.height / 500);
  ctx.translate(199, 241);
  ctx.rotate(-0.17);

  function line(x, y, endX, endY, color, width, dash = []) {
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(endX, endY);
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.setLineDash(dash);
    ctx.stroke();
  }

  function shape(x, y, width, height, radius, color) {
    ctx.beginPath();
    ctx.roundRect(x, y, width, height, radius);
    ctx.fillStyle = color;
    ctx.fill();
  }

  function car(x, y, angle, color) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);
    for (const side of [-15, 10]) {
      shape(side, -19, 5, 14, 2, '#07182b');
      shape(side, 15, 5, 14, 2, '#07182b');
    }
    shape(-13, -33, 26, 66, 7, color);
    shape(-10, -17, 20, 35, 4, '#183b57');
    shape(-10, -12, 20, 21, 4, color);
    shape(-9, -28, 5, 4, 1, '#f1f7fb');
    shape(4, -28, 5, 4, 1, '#f1f7fb');
    shape(-8, 26, 4, 3, 1, '#a7453a');
    shape(4, 26, 4, 3, 1, '#a7453a');
    ctx.restore();
  }

  ctx.fillStyle = '#183652';
  ctx.fillRect(-275, -62, 550, 124);
  ctx.fillRect(-55, -300, 110, 600);
  for (const y of [-62, 62]) {
    line(-265, y, -55, y, '#436685', 2);
    line(55, y, 265, y, '#436685', 2);
  }
  for (const x of [-55, 55]) {
    line(x, -288, x, -62, '#436685', 2);
    line(x, 62, x, 288, '#436685', 2);
  }
  for (const [x, y, endX, endY] of [[-260, 0, -62, 0], [62, 0, 260, 0], [0, -290, 0, -68], [0, 68, 0, 290]]) {
    line(x, y, endX, endY, '#7999b1', 3, [15, 13]);
  }
  car(-46, 17, Math.PI / 2 + 0.12, '#e6eef3');
  car(10, -37, Math.PI + 0.15, '#84b3d7');
  for (const [x, y, endX, endY] of [[-3, 2, -16, -8], [2, 4, 11, -7], [4, 12, 19, 13], [1, 18, 7, 32]]) {
    line(x, y, endX, endY, '#f0b571', 3);
  }
}

window.deckOptions = {
  plugins: [RevealNotes],
  transition: 'none',
  pdfSeparateFragments: false,
  pdfMaxPagesPerSlide: 1
};
