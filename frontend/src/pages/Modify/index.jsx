import { useEffect, useState } from "react";
import { BookModi } from "./layout/BookModi";
import { DramaModi } from "./layout/DramaModi";
import { useParams } from "react-router-dom";
import { MovieModi } from "./layout/MovieModi";
import axios from "../../api/axios";

export const Modify = () => {
  const { id } = useParams();

  const [quote, setQuote] = useState(null);
  const [source,setSource] =useState(null);

  useEffect(() => {
    const fetchQuote = async () => {
      try {
        // TODO: /api/quote/${id}, no navigation
        const response = await axios.get(`/quote/${id}`);
        console.log(`/api/quote/${id}`, response);
        setQuote(response.data);
        const sourceID = response.data.source_id;
        try {
          const data = await axios.get(`/source/${sourceID}`);
          console.log(data.data);
          setSource(data.data);
          }
          catch(e){
            console.log('Failed to fetch sourceData',e);
          }
      } catch (error) {
        console.error("Failed to fetch quote:", error);
      }
    };

    fetchQuote();
  }, [id]);

  return (
    <>
      {quote ?(
        <>
          {source?.source_type === "book" && <BookModi quote={quote} source={source}/>}
          {source?.source_type === "drama" && <DramaModi quote={quote} source={source}/>}
          {source?.source_type === "movie" && <MovieModi quote={quote} source={source}/>}
        </>
      ):
      <div>
        잘못된 접근입니다.</div>}
      
    </>
  );
};
