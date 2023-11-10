import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginPageComponent } from './authentication/login-page/login-page.component'
import {SessionsOverviewComponent} from "./chat/sessions-overview/sessions-overview.component";
import {ChatPage} from "./chat/chat-page/chat.page";

const routes: Routes = [
  {
    path: 'login',
    component: LoginPageComponent
  },
  {
    path: 'chat',
    component: ChatPage
  },
  {path: '', redirectTo: 'chat', pathMatch: 'full'},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
