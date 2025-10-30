import { useNavigate } from "react-router-dom";
import mark from "../../../assets/bookmark.png";
import marked from "../../../assets/bookmark_marked.png";
import { useEffect, useState } from "react";
import axios from "../../../api/axios";
import { useBookmarks } from '../../../hooks/useBookmarks';

export const BookDetail = ({ quote }) => {
  const navigation = useNavigate();
  const [isLogin, setIsLogin] = useState(false);
  const [bookmark, setBookMarked] = useState(false);
  const [user, setUser] = useState({});
  const [source, setSource] = useState({});
  const [publisherName, setPublisherName] = useState(""); // 출판사 이름 저장용

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem("accessToken");
      console.log(token);
      console.log(quote);

      const id = quote.source_id;
      console.log(id);

      const sourceData = await axios.get(`/api/source/${id}`);
      setSource(sourceData.data);
      console.log(sourceData.data);

      if (sourceData.data.publisher_id) {
        const publisherID = await axios.get(`/api/publisher/${sourceData.data.publisher_id}`);
        setPublisherName(publisherID.data.name);
      }

      if (token) {
        // TODO: /api/auth/me - need testing
        const response = await axios.get("/api/auth/me", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        console.log("/api/auth/me", response);
        const userData = response.data;
        setUser(userData);
        setIsLogin(true);
        // console.log(user);
        // Check if the current quote is bookmarked by the user
        // user에 bookmark가 없음
        // const bookmarkCheck = await axios.
        const isBookmarked =
          userData.bookmarks?.some((b) => b.quote_id === quote.id) ?? false;
        setBookMarked(isBookmarked);
      } else {
        setIsLogin(false);
      }
    };

    fetchUser();
  }, [isLogin, quote.id]);

  const onIsLogin = async () => {
    console.log(isLogin);
    if (!isLogin) {
      alert("로그인이 필요한 기능입니다.");
      return;
    }

    const token = localStorage.getItem("accessToken");

    if (bookmark) {
      // Unbookmark
      // TODO: /api/bookmark/?user_id=${user.id}&quote_id=${quote.id} - need testing
      const response = await axios.delete(
        `/api/bookmark/?user_id=${user.id}&quote_id=${quote.id}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      console.log(
        `/api/bookmark/?user_id=${user.id}&quote_id=${quote.id}`,
        response
      );
      setBookMarked(false);
    } else {
      // Bookmark
      // TODO: /api/bookmark/ - need testing
      const response = await axios.post(
        "/api/bookmark/",
        { user_id: user.id, quote_id: quote.id },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );
      console.log("/api/bookmark/", response);
      setBookMarked(true);
    }
  };

  const onSearchList = (input) => {
    navigation("/searchlist/" + input);
  };

  const onModify = () => {
    navigation("/detail/" + quote.id + "/modi");
  };

  const onDelete = () => {
    //TODO: make delete
  };

  return (
    <>
      <div className="flex flex-col mt-10">
        <div className="text-3xl mb-5">BOOK MOMENT</div>
        {(isLogin && user.id == quote.writer) && (
          <div className="text-end">
            <button
              className="px-4 py-2 rounded-lg border hover:bg-main-beige border-main-green text-xs mr-2"
              onClick={onModify}
            >
              수정
            </button>
            <button
              className="px-4 py-2 rounded-lg border hover:bg-main-beige border-main-green text-xs"
              onClick={onDelete}
            >
              삭제
            </button>
          </div>
        )}

        <div className="flex items-end mt-3">
          <label className="w-1/12 text-sm text-end pb-3">책 제목 </label>
          <div className="w-4/6 text-start text-xl rounded-lg p-2 pl-4 ml-3">
            <span className="cursor-pointer" onClick={() => onSearchList(source.title)}>
              {source.title}
            </span>
          </div>
        </div>

        <div className="flex justify-center mt-3">
          <div className="w-4/5 text-main-white pt-12 pb-12 bg-main-green rounded-lg p-2 pl-4 ml-3 shadow-lg shadow-gray-400">
            {quote.content}
          </div>
        </div>

        <div className="flex justify-end mt-3">
          <div className="flex border-2 border-sub-darkgreen rounded-lg p-3 mr-14">
            <img className="size-5 cursor-pointer" onClick={onIsLogin} src={(isLogin&&bookmark)?marked:mark}/>
          </div>
        </div>

        <div className="flex items-end mt-3">
          <label className="w-1/12 text-end pb-3 text-sm">저자 </label>
          <div className="w-4/6 text-start rounded-lg p-2 pl-4 ml-3 text-sm pb-3">
            <span className="cursor-pointer" onClick={() => onSearchList(source.creator)}>
              {source.creator}
            </span>
          </div>
        </div>

        {source.publisher_id && (
          <>
            <div className="flex items-end mt-3">
              <label className="w-1/12 text-end pb-3 text-sm">출판사 </label>
              <div className="w-4/6 text-start rounded-lg p-2 pl-4 ml-3 text-sm pb-3">
                {publisherName || "출판사 정보 없음"}
              </div>
            </div>
          </>
        )}

        {/* tag 조회 */}
        {quote.tags && (
          <div className="flex items-end mt-3">
            <label className="w-1/12 text-end text-sm pb-3">TAGS </label>
            <div className="w-4/6 text-start rounded-lg p-2 pl-4 ">
              {quote.tags.map((t) => (
                <span
                  key={String(t?.id ?? t)}
                  onClick={() => onSearchList(t)}
                  className="cursor-pointer rounded-xl p-2 bg-main-beige text-xs ml-1 mr-1 mb-1 border-sub-darkbeidge border"
                >
                  {String(t?.name ?? t)}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </>
  );
};
