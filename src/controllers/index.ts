class IndexController {
    getIndex(req, res) {
        res.send('Welcome to the YOLO Collaboration Project!');
    }

    postItem(req, res) {
        const item = req.body;
        // Logic to handle the posted item
        res.status(201).send(item);
    }

    // Additional methods can be added here as needed
}

export default IndexController;