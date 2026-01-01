import { useNavigate, useParams } from "react-router-dom";
import { BookMark } from "./layout/BookMark";
import { Upload } from "./layout/Upload";
import { MemberInfo } from "./layout/MemberInfo";
import { useAuth } from "../../hooks/useAuth";

export const Mypage = () => {
    const { tab } = useParams();
    const navigate = useNavigate();
    const { user } = useAuth();

    const menuStyle = (isActive) =>
        `flex-1 text-center py-3 text-sm transition-colors duration-200 ${isActive ? "bg-mypage-menu font-bold text-gray-800" : "text-gray-500 hover:bg-gray-50 text-gray-500"
        }`;

    return (
        <div className="flex flex-col md:flex-row mt-4 md:mt-8 min-h-[60vh]">
            {/* Sidebar / Top Tab */}
            <div className="w-full md:w-2/12 border-b-2 md:border-b-0 md:border-r-2 border-main-green h-auto md:h-screen">
                <ul className="flex flex-row md:flex-col items-stretch">
                    <li className={menuStyle(tab === "memberinfo")} onClick={() => navigate("/mypage/memberinfo")}>
                        회원정보
                    </li>
                    <li className={menuStyle(tab === "bookmark")} onClick={() => navigate("/mypage/bookmark")}>
                        북마크
                    </li>
                    <li className={menuStyle(tab === "upload")} onClick={() => navigate("/mypage/upload")}>
                        업로드한 글
                    </li>
                </ul>
            </div>

            <div className="w-full md:w-10/12 p-2 md:p-6">
                {tab === "bookmark" && user && <BookMark userId={user.id} />}
                {tab === "memberinfo" && <MemberInfo />}
                {tab === "upload" && user && <Upload userId={user.id} />}
            </div>
        </div>
    );
}