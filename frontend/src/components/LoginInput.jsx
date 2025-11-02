export const LoginInput = ({ title, type, name ,error}) => {

  return (
    <>
      <div>
        <div className="text-white">{title}</div>
        <div>
          <input type={type} name={name} className={`border-2 
            ${error ? "border-red-500 focus:border-red-500" : "border-gray-300 focus:border-main-green"}
          bg-white`} />
        </div>
      </div>
    </>
  );
};
