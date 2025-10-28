import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { BookDetail } from "./layout/BookDetail";
import { MovieDetail } from "./layout/MovieDetail";
import { DramaDetail } from "./layout/DramaDetail";
import { RecommendDetail } from "./layout/RecommendDetail";

export const Detail=()=>{
    /** id로 해당 data 불러오기  */
    const {id} = useParams();    
    const [mode, setMode]=useState('');
    const [quote,setQuote]=useState('');

    // TODO: API call here
    /** dummy data */
    useEffect(()=>{
        const q = {'id':0,'category':0,
            'title':'title','creater':'author book','subData':'',
            'content':'content contentcontentcontentcontentcontent',
            'tags':['warm','hope'],
            'writer':'user1', 'createdAt':'2013-10-23'
        }
        setQuote(q);
        setMode('book');
    },[id]);

    return(
        <>
        {mode=='book'&& <BookDetail quote={quote}/>}
        {mode=='movie'&& <MovieDetail quote={quote}/>}
        {mode=='drama'&& <DramaDetail quote={quote}/>}
        <RecommendDetail quote={quote}/>
        </>
    );
}