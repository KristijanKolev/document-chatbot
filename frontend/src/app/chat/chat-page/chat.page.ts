import {Component, OnInit} from '@angular/core';
import {ChatService} from "../chat.service";
import {ChatSessionSimple} from "../../models/chatSessionSimple";
import {ChatSession} from "../../models/chatSession";

@Component({
  selector: 'app-chat-page',
  templateUrl: './chat.page.html',
  styleUrls: ['./chat.page.css']
})
export class ChatPage implements OnInit{
  allSessions: ChatSessionSimple[] = [];
  selectedSession?: ChatSession = undefined;

  constructor(
    private chatService: ChatService
  ) { }

  ngOnInit(): void {
    this.chatService.loadChatSessions().subscribe({
      next: sessions => this.allSessions = sessions,
      error: err => console.log('ERROR: ', err),
    })
  }

  onSessionSelected(session: ChatSessionSimple) {
    this.chatService.loadChatSessionDetails(session.id).subscribe({
      next: value => this.selectedSession = value,
      error: err => {
        alert(err);
        this.selectedSession = undefined;
      }
    })
  }
}
