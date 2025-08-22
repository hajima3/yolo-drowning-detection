import { IndexController } from '../src/controllers/index';
import request from 'supertest';
import express from 'express';

const app = express();
const indexController = new IndexController();

app.use(express.json());
app.get('/', indexController.getIndex.bind(indexController));
app.post('/items', indexController.postItem.bind(indexController));

describe('IndexController', () => {
    it('should return a 200 response for GET /', async () => {
        const response = await request(app).get('/');
        expect(response.status).toBe(200);
    });

    it('should create an item and return a 201 response for POST /items', async () => {
        const newItem = { name: 'Test Item' };
        const response = await request(app).post('/items').send(newItem);
        expect(response.status).toBe(201);
        expect(response.body).toHaveProperty('id');
        expect(response.body.name).toBe(newItem.name);
    });
});