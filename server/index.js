const express = require('express');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const app = express();
app.use(express.json());

app.post('/webhook', (req, res) => {
    const data = req.body;

    // Guarda la orden en archivo JSON
    const filePath = path.join(__dirname, 'orders', 'last_order.json');
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));

    // Ejecuta el script Python
    exec('python3 ../bot/trader.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error ejecutando Python: ${error.message}`);
            return res.status(500).send('Error ejecutando la orden');
        }
        console.log(`Resultado Python: ${stdout}`);
        res.send('Orden ejecutada correctamente');
    });
});

app.listen(3000, () => {
    console.log('Servidor Webhook corriendo en http://localhost:3000');
});
