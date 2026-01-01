import { useState } from "react";
import { useAuth } from "./useAuth";
import { getAIRecommendations } from "../api/recommendation";

export const useAIRecommendation = () => {
    const { user, showAlert } = useAuth();
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchRecommendations = async (refresh = false) => {
        if (!user) {
            showAlert("로그인이 필요한 서비스입니다.");
            return;
        }

        setLoading(true);
        setError(null);

        if (refresh) {
            setRecommendations([]);
        }

        try {
            const response = await getAIRecommendations(refresh);
            let data = response.data;

            // Normalize data (handle string or array)
            if (typeof data === 'string') {
                try {
                    data = JSON.parse(data);
                } catch (e) {
                    // If not JSON, wrapped in a list as a reason?
                    data = [{ title: "AI 메시지", reason: data }];
                }
            }

            setRecommendations(Array.isArray(data) ? data : [data]);
        } catch (err) {
            setError("추천을 가져오는 중 오류가 발생했습니다.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return { recommendations, loading, error, fetchRecommendations };
};
