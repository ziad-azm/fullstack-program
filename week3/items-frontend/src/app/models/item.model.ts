export interface Item {
  id: number;
  name: string;
  price: number;
  in_stock: boolean;
  created_at: string;
}

export interface ItemCreate {
  name: string;
  price: number;
  in_stock?: boolean;
}
