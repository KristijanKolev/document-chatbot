import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { NgbModule} from "@ng-bootstrap/ng-bootstrap";
import {CookieService} from 'ngx-cookie-service';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthenticationModule } from "./authentication/authentication.module";
import {HttpClientModule} from "@angular/common/http";
import {authInterceptorProviders} from "./authentication/interceptors/auth-interceptor";
import {ChatModule} from "./chat/chat.module";
import {authErrorInterceptorProviders} from "./authentication/interceptors/error-interceptor";

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    HttpClientModule,
    AuthenticationModule,
    ChatModule
  ],
  providers: [
    CookieService,
    authInterceptorProviders,
    authErrorInterceptorProviders,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
