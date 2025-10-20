import React from "react";

const SigninInput = ({ title, ...inputProps }, ref) => {
  return (
    <>
     
        <div className="mb-3 flex flex-col sm:flex-row sm:items-center sm:justify-end">
          <div className="mb-3 whitespace-nowrap">{title}</div>
          <div>
            <input
              {...inputProps}
              ref={ref}
              className="ml-3 w-full sm:w-[300px] bg-white rounded-md shadow-md focus:shadow-lg focus:outline-none p-2"
            />
          </div>
        </div>

    </>
  );
};

export default SigninInput;
