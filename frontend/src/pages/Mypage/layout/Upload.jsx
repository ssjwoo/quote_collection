import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../../../api/axios";

export const Upload = () => {
  const navigation = useNavigate();
  const [quotes, setQuotes] = useState([]);

  useEffect(() => {
    const fetchUserAndQuotes = async () => {
      try {
        const token = localStorage.getItem("token");
        if (token) {
          // TODO: /api/auth/me
          const userResponse = await axios.get("/api/auth/me", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          console.log("/api/auth/me", userResponse);
          const userData = userResponse.data;
          // TODO: /api/users/${userData.id}/quotes
          const quotesResponse = await axios.get(
            `/api/users/${userData.id}/quotes`
          );
          console.log(`/api/users/${userData.id}/quotes`, quotesResponse);
          setQuotes(quotesResponse.data);
        } else {
          // Handle case where user is not logged in
        }
      } catch (error) {
        console.error("Failed to fetch data:", error);
      }
    };

    fetchUserAndQuotes();
  }, []);

  const onDetail = (id) => {
    navigation("/detail/" + id);
  };
    return(
        <>
        <div className="flex flex-col justify-items-center m-3">
            {quotes.map((q)=>(
        <div key={q.id} className=" cursor-pointer mt-5 border-2 hover:bg-main-beige border-main-green h-full pt-5 pb-5 text-center rounded-lg shadow-lg" 
        onClick={() => onDetail(q.id)}> 
            <div className=" pl-3 pb-3 text-sm text-start">{q.title} </div>
            <div className="text-lg">{q.content}</div>
            <div className="text-xs text-end pr-3"><span className="mr-2 font-bold">{q.creater}</span>{q.createdAt}</div>
          </div>
        ))}
        </div>
        </>
    );
}