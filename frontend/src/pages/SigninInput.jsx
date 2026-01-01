import React from "react";

const SigninInput = ({ title, ...inputProps }, ref) => {
  return (
    <>

      <div className="mb-4 flex flex-col sm:flex-row sm:items-center sm:justify-end w-full">
        <div className="mb-1 sm:mb-0 sm:mr-4 whitespace-nowrap text-left sm:text-right min-w-[80px]">{title}</div>
        <div className="w-full sm:w-auto flex-1">
          <input
            {...inputProps}
            ref={ref}
            className="w-full sm:w-[300px] bg-white rounded-md shadow-md focus:shadow-lg focus:outline-none p-3 sm:p-2 border border-transparent focus:border-main-green transition-all"
          />
        </div>
      </div>

    </>
  );
};

export default SigninInput;
