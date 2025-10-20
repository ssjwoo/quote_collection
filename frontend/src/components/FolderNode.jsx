import CreateButton from "./CreateButton";

export default function FolderNode({ node, addAtId, onRequestCreateAt }) {
  return (
    <div className="ml-2">
      <div className="inline-flex gap-2 px-2 py-1 rounded border-2 border-custom-basic-font bg-custom-search">
        <span className="font-medium">{node.name}</span>
      </div>

      <div className="ml-4 mt-2 space-y-2">
        {node.children.map((child) => (
          <FolderNode
            className=''
            key={child.id}
            node={child}
            addAtId={addAtId}
            onRequestCreateAt={onRequestCreateAt}
          />
        ))}

        {node.id === addAtId && (
          <CreateButton onClick={() => onRequestCreateAt(node.id)} />
        )}
      </div>
    </div>
  );
}
