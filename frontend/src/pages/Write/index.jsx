import { useState } from "react";

import { MovieWrite } from "./layout/MovieWrite";
import { DramaWrite } from "./layout/DramaWrite";
import { BookWrite } from "./layout/BookWrite";

export const Write = () =>{

    const [mode, setMode]=useState("book");
    const style = ["w-2/12 ml-6 mr-6 cursor-pointer","ml-6 mr-6 cursor-pointer border-b-4 border-main-green pb-2 w-2/12"];

    return(
        <>
        <ul className="flex flex-row justify-center mt-3">
            <li className={mode=='book'?style[1]:style[0]} onClick={()=>setMode('book')}> book </li>
            <li className={mode=='movie'?style[1]:style[0]} onClick={()=>setMode('movie')}> movie </li>
            <li className={mode=='drama'?style[1]:style[0]} onClick={()=>setMode('drama')}> drama </li>
        </ul>

        {mode == 'book'&& <BookWrite/>}
        {mode == 'movie'&& <MovieWrite/>}
        {mode == 'drama'&& <DramaWrite/>}
        </>
    );
}