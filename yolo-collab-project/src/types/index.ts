export interface Request {
    body: any;
    params: { [key: string]: string };
    query: { [key: string]: string };
}

export interface Response {
    status: (statusCode: number) => Response;
    json: (body: any) => void;
    send: (body: any) => void;
}