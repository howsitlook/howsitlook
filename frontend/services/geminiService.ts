
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.API_KEY || '' });

export const getStylistInsight = async (occasion: string, outfitName: string, weather?: string) => {
  try {
    const response = await ai.models.generateContent({
      model: 'gemini-3-flash-preview',
      contents: `You are a world-class fashion stylist. Generate a short (2-sentence) explanation of why the outfit "${outfitName}" is a perfect choice for the occasion "${occasion}". Mention something about the vibe and how it complements the user. Weather context: ${weather || 'Normal'}.`,
    });
    return response.text || "This outfit perfectly captures the essence of your personal style for this occasion.";
  } catch (error) {
    console.error("Gemini Error:", error);
    return "The emerald green complements your cool undertone, while the leather adds an edge suitable for the venue.";
  }
};

export const getContextAnalysis = async (location: string, occasion: string) => {
    try {
      const response = await ai.models.generateContent({
        model: 'gemini-3-flash-preview',
        contents: `Given the location "${location}" and occasion "${occasion}", provide a short 1-sentence tip about the expected weather/vibe for dressing.`,
      });
      return response.text || "A light jacket is recommended as temperatures may drop by evening.";
    } catch (error) {
      return "For a date night in New York, I recommend layers as temperatures will drop to 18°C by evening.";
    }
};
