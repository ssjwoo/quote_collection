export const LoginInput = ({ title, type, name }) => {
  return (
    <>
      <div>
        <div className="text-white">{title}</div>
        <div>
          <input type={type} name={name} className="pl-1 bg-white" />
        </div>
      </div>
    </>
  );
};
