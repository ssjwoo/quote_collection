import axios from "./axios";

export const getAIRecommendations = async (refresh = false) => {
  const url = refresh ? "/recommendations/ai?refresh=true" : "/recommendations/ai";
  const response = await axios.post(url, {}, { timeout: 60000 });
  return response;
};
