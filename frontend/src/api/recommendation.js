import axios from "./axios";

export const getAIRecommendations = async () => {
  const response = await axios.post("/recommendations/ai", {}, { timeout: 60000 });
  return response;
};
