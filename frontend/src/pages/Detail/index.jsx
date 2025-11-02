import { useEffect, useState } from "react";
import { useLocation, useParams } from "react-router-dom";
import { BookDetail } from "./layout/BookDetail";
import { MovieDetail } from "./layout/MovieDetail";
import { DramaDetail } from "./layout/DramaDetail";
import { RecommendDetail } from "./layout/RecommendDetail";
import axios from "../../api/axios";

export const Detail = () => {
  const { id } = useParams();
  const [quote, setQuote] = useState(null);

  useEffect(() => {
    const fetchQuote = async () => {
      try {
        const response = await axios.get(`/quote/${id}`);
        setQuote(response.data);
      } catch (error) {
        console.error("Failed to fetch quote:", error);
      }
    };

    fetchQuote();
  }, [id]);

  if (!quote || !quote.source) {
    return <div>Loading...</div>; 
  }

  const mode = quote.source.source_type;

  return (
    <>
      {mode === "book" && <BookDetail quote={quote} />}
      {mode === "movie" && <MovieDetail quote={quote} />}
      {mode === "drama" && <DramaDetail quote={quote} />}
      <RecommendDetail mode={mode} quote={quote} />
    </>
  );
};
