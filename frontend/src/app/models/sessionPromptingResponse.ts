import {ChatPrompt} from "./chatPrompt";

export interface SessionPromptingResponse {
  prompt: ChatPrompt,
  session_updated: boolean,
}
