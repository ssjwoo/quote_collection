import { useNavigate } from "react-router-dom";

export const Logo=()=>{

    const navigator = useNavigate();

    return(
        <>
        {/* <hr className="border-1"></hr> */}
        <div className="flex justify-center mt-7 mb-10 cursor-pointer"
        ><span className="text-3xl text-center rounded-full border-2 px-4 py-1" onClick={()=>navigator('/')}>MOMENTARY</span></div>
        <hr className=" border-1"></hr>
        </>
    );
}