import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
    build: {
        rollupOptions: {
            input: {
                main: resolve(__dirname, 'index.html'),
                abc: resolve(__dirname, 'producto-abc.html'),
                abm: resolve(__dirname, 'producto-abm.html'),
                abp: resolve(__dirname, 'producto-abp.html'),
                bolsas: resolve(__dirname, 'producto-bolsas.html'),
                desengrasante: resolve(__dirname, 'producto-desengrasante.html'),
                diatomeas: resolve(__dirname, 'producto-diatomeas.html'),
                kits: resolve(__dirname, 'producto-kits.html'),
                pallets: resolve(__dirname, 'producto-pallets.html'),
                quimicos: resolve(__dirname, 'producto-quimicos.html'),
            },
        },
    },
});
