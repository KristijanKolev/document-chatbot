import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {User} from "../models/user";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  public token?: string = undefined;

  constructor(
    private http: HttpClient
  ) { }

  public getCurrentUser(token: string): Observable<User> {
    const headers: HttpHeaders = new HttpHeaders({
      Authorization: `Bearer ${token}`
    })
    return this.http.get<User>('/api/users/me', {headers: headers})
  }

  setToken(token?: string) {
    this.token = token;
  }
}
