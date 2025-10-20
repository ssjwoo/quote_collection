import { useNavigate, useParams } from "react-router-dom";
import { BookMark } from "./layout/BookMark";
import { Upload } from "./layout/Upload";
import { MemberInfo } from "./layout/MemberInfo";

export const Mypage=()=>{
    const { tab } = useParams(); 
    const navigate = useNavigate();

    const style = ["mt-10 text-sm pt-3 pb-3 ml-1" ,"mt-10 text-sm bg-main-white pt-3 pb-3 mr-5 rounded-lg"];

    return(
        <div className="flex flex-row mt-8">
            <div className="w-2/12 border-r-2 border-main-green pr-3 h-screen">
                <ul>
                    <li className={tab === "memberinfo" ? style[1] : style[0]} onClick={() => navigate("/mypage/memberinfo")}>회원정보</li>
                    <li className={tab === "bookmark" ? style[1] : style[0]} onClick={() => navigate("/mypage/bookmark")}>북마크</li>
                    <li className={tab === "upload" ? style[1] : style[0]} onClick={() => navigate("/mypage/upload")}>업로드한 글</li>
                </ul>
            </div>
        
            <div className="w-5/6">
                {tab === "bookmark" && <BookMark />}
                {tab === "memberinfo" && <MemberInfo />}
                {tab === "upload" && <Upload />}
            </div>
        </div>
    );
}