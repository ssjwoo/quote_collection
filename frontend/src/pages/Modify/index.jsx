import { useEffect, useState } from "react";
import { BookModi } from "./layout/BookModi";
import { DramaModi } from "./layout/DramaModi";
import { useParams } from "react-router-dom";
import { MovieModi } from './layout/MovieModi';

export const Modify =()=>{
    const{id}=useParams();

    /**id 이용해서 quote 정보 가져오기 */
    // TODO: API call here
    /**dummy */
    const [quote,setQuote] = useState({});
    
    useEffect(()=>{
        // setQuote({'id':id,sourceType:'book',title:'HarryPotter',creater:'JK ROWling', subdata:'magic box', content:'shut up malfoy \n\n - Harry',tags:['용기','성장']});
        setQuote({'id':id,sourceType:'movie',title:'HarryPotter',creater:'JK ROWling', subdata:'2011', content:'shut up malfoy \n\n - Harry',tags:['판타지','해외']});
    },[]);

    return(
        <>
        {(quote.sourceType == 'book') && <BookModi quote = {quote} />}
        {(quote.sourceType == 'drama') && <DramaModi quote = {quote} />}
        {(quote.sourceType == 'movie') && <MovieModi quote = {quote} />}
        </>
    );
}