import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../../../api/axios";
import { Pagination } from "../../../components/Pagination";

export const BookMark = ({ userId }) => {
  const navigation = useNavigate();
  const [quotes, setQuotes] = useState([]);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!userId) return;

    const fetchBookmarkedQuotes = async () => {
      setIsLoading(true);
      try {
        const response = await axios.get(`/bookmark/user/${userId}?page=${currentPage}&size=10`);
        setQuotes(response.data.items);
        setTotal(response.data.total);
        setTotalPages(response.data.total_pages);
      } catch (error) {
        console.error("Failed to fetch bookmarked quotes:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchBookmarkedQuotes();
  }, [userId, currentPage]);

  const onDetail = (id) => {
    navigation("/quote/" + id);
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
    window.scrollTo(0, 0);
  };

  return (
    <div className="p-6 mt-4 mx-auto max-w-6xl">
      <h1 className="text-3xl font-medium mb-6 text-center">My Bookmarks</h1>

      <div className="mb-4 text-right text-sm text-gray-500">
        전체 {total}개
      </div>

      <div className="flex flex-col justify-items-center m-3 min-h-[400px]">
        {isLoading ? (
          <div className="flex justify-center items-center h-40">Loading...</div>
        ) : quotes.length > 0 ? (
          <>
            {quotes.map((q) => (
              <div
                key={q.id}
                className="cursor-pointer mt-5 border-2 hover:bg-mypage-menu/50 border-main-green h-full pt-5 pb-5 text-center rounded-lg shadow-lg active:scale-[0.98] transition-all"
                onClick={() => onDetail(q.id)}
              >
                <div className="text-lg px-4">{q.content}</div>
                {q.source && (
                  <div className="text-sm text-gray-500 mt-2">
                    - {q.source.title} ({q.source.creator})
                  </div>
                )}
              </div>
            ))}

            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={handlePageChange}
            />
          </>
        ) : (
          <p className="text-center py-10 text-gray-400">북마크한 인용문이 없습니다.</p>
        )}
      </div>
    </div>
  );
};
