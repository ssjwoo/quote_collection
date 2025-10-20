export const newBookmark = (name) => ({
  id:
    (crypto?.randomUUID ? crypto.randomUUID() : Date.now() + Math.random().toString(16).slice(2)),
  name,
  children: [],
});

export const addMark = (node, targetId, child) => {
  if (node.id === targetId) return { ...node, children: [...node.children, child] };
  return { ...node, children: node.children.map((c) => addMark(c, targetId, child)) };
};
