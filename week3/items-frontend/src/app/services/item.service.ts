import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import { Item, ItemCreate } from '../models/item.model';

@Injectable({
  providedIn: 'root',
})
export class ItemService {
  private readonly baseUrl = `${environment.apiUrl}/items`;

  constructor(private readonly http: HttpClient) {}

  getItems(): Observable<Item[]> {
    return this.http.get<Item[]>(this.baseUrl);
  }

  createItem(payload: ItemCreate): Observable<Item> {
    return this.http.post<Item>(this.baseUrl, payload);
  }
}
