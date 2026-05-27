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
                anaerobicos: resolve(__dirname, 'productos-anaerobicos.html'),
                cianoacrilatos: resolve(__dirname, 'productos-cianoacrilatos.html'),
                selladores: resolve(__dirname, 'productos-selladores.html'),
                adhesivos: resolve(__dirname, 'productos-adhesivos.html'),
                lubricantes: resolve(__dirname, 'productos-lubricantes.html'),
                limpiamanos: resolve(__dirname, 'productos-limpiamanos.html'),
            },
        },
    },
});
