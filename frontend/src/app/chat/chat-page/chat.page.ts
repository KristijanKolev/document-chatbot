import {Component, OnInit} from '@angular/core';
import {ChatService} from "../chat.service";
import {ChatSessionSimple} from "../../models/chatSessionSimple";
import {ChatSession} from "../../models/chatSession";
import {ChatPrompt} from "../../models/chatPrompt";

@Component({
  selector: 'app-chat-page',
  templateUrl: './chat.page.html',
  styleUrls: ['./chat.page.css']
})
export class ChatPage {
  allSessions: ChatSessionSimple[] = [];
  selectedSession?: ChatSession = undefined;

  constructor(
    private chatService: ChatService
  ) { }

  onSessionSelected(session: ChatSessionSimple) {
    this.chatService.loadChatSessionDetails(session.id).subscribe({
      next: value => this.selectedSession = value,
      error: err => {
        alert(err);
        this.selectedSession = undefined;
      }
    });
  }

  createPrompt(promptText: string) {
    if (this.selectedSession) {
      let newPrompt: ChatPrompt = {
        prompt: promptText,
        answer: undefined,
        session_id: this.selectedSession?.id,
        created_at: undefined,
      }
      this.selectedSession.prompts.push(newPrompt);
      this.chatService.createPrompt(this.selectedSession.id, promptText).subscribe({
        next: answeredPrompt => {
          if (this.selectedSession) {
            const lastPromptIndex = this.selectedSession.prompts.length - 1;
            this.selectedSession.prompts[lastPromptIndex] = answeredPrompt;
          }
        },
        error: err => {
          alert(err);
          // @ts-ignore
          this.selectedSession.prompts.pop();
        }
      });
    }
  }
}
