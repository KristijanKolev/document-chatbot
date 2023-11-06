import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {User} from "../models/user";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  public token = null;

  constructor(
    private http: HttpClient
  ) { }

  public get_current_user_details(token: string): Observable<User> {
    const headers: HttpHeaders = new HttpHeaders({
      Authorization: `Bearer ${token}`
    })
    return this.http.get<User>('/api/users/me', {headers: headers})
  }
}