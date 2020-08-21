// Draw progress bars
const canvases = document.getElementsByClassName("progress");
for (let i = 0; i < canvases.length; i++) {
  const canvas = canvases[i];
  const ctx = canvas.getContext('2d');

  const currentPage = canvas.dataset.current;
  const totalPages = canvas.dataset.total;
  const max_width = canvas.width;
  const height = canvas.height;
  const progress = max_width/totalPages * currentPage;

  ctx.save();
  ctx.fillStyle = "#10ff10";
  ctx.fillRect(0, 0, progress, height);
  ctx.strokeStyle = "#bfbfbf";
  ctx.lineWidth = 2;
  offset = ctx.lineWidth * 2;
  ctx.strokeRect(0, 0, max_width, height);

  ctx.fillStyle = "#333";
  ctx.font = '15px sans-serif';
  const pagesText = currentPage + ' pages out of ' + totalPages + ' read';
  ctx.textAlign = 'center';
  ctx.fillText(pagesText, max_width/2, 17);

  ctx.restore();
};
