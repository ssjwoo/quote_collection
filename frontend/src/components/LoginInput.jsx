export const LoginInput = ({ title, type, name }) => {
  return (
    <>
      <div>
        <div className="text-white">{title}</div>
        <div>
          <input type={type} name={name} className="bg-white" />
        </div>
      </div>
    </>
  );
};
