import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../../../api/axios";

export const Upload = ({ userId }) => {
  const navigation = useNavigate();
  const [quotes, setQuotes] = useState([]);
  const [sort, setSort] = useState("recent");

  useEffect(() => {
    if (!userId) return;

    const fetchQuotes = async () => {
      try {
        const response = await axios.get(`/quote/user/${userId}`);
        setQuotes(response.data);
      } catch (error) {
        console.error("Failed to fetch uploaded quotes:", error);
      }
    };

    fetchQuotes();
  }, [userId]);

  const sortedQuotes = useMemo(() => {
    return [...quotes].sort((a, b) => {
      if (sort === "recent") {
        return new Date(b.created_at) - new Date(a.created_at);
      }
      if (sort === "alpha") {
        return a.content.localeCompare(b.content);
      }
      return 0;
    });
  }, [quotes, sort]);

  const onDetail = (id) => {
    navigation("/quote/" + id);
  };

  return (
    <>
      <div className="mb-8 flex flex-col items-end gap-3">
        <div className="flex items-center gap-2">
          <label className="text-sm">정렬</label>
          <select
            className="text-sm border rounded px-2 py-2"
            value={sort}
            onChange={(e) => setSort(e.target.value)}
          >
            <option value="recent">최신순</option>
            <option value="alpha">가나다순</option>
          </select>
        </div>
      </div>
      <div className="flex flex-col justify-items-center m-3">
        {sortedQuotes.length > 0 ? (
          sortedQuotes.map((q) => (
            <div
              key={q.id}
              className="cursor-pointer mt-5 border-2 hover:bg-mypage-menu/50 border-main-green h-full pt-5 pb-5 text-center rounded-lg shadow-lg"
              onClick={() => onDetail(q.id)}
            >
              <div className="text-lg">{q.content}</div>
            </div>
          ))
        ) : (
          <p>업로드한 인용문이 없습니다.</p>
        )}
      </div>
    </>
  );
};
