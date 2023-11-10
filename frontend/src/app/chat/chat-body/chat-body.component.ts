import {Component, EventEmitter, Input, OnChanges, Output, SimpleChanges} from '@angular/core';
import {ChatSession} from "../../models/chatSession";

@Component({
  selector: 'app-chat-body',
  templateUrl: './chat-body.component.html',
  styleUrls: ['./chat-body.component.css']
})
export class ChatBodyComponent implements OnChanges {
  @Input() chatSession?: ChatSession;
  @Output() onPrompt: EventEmitter<string> = new EventEmitter<string>();

  newPromptText: string = '';

  ngOnChanges(changes: SimpleChanges): void {
    let newSession = changes['chatSession'];

    console.log(this.chatSession);

    if (newSession) {
      this.newPromptText = '';
    }
  }

  sendPrompt() {
    this.onPrompt.emit(this.newPromptText);
    this.newPromptText = '';
  }
}
