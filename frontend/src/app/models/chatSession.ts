import {ChatSessionSimple} from "./chatSessionSimple";
import {ChatPrompt} from "./chatPrompt";

export interface ChatSession extends ChatSessionSimple{
  prompts: ChatPrompt[]
}
