<?php

namespace Database\Seeders;

use App\Models\UserSetting;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $this->call([
            EventSeeder::class,
        ]);

        UserSetting::firstOrCreate([], [
            'objetivo' => 'autorregulacion',
            'modo_anonimo' => false,
            'alerta_sintomas' => true,
        ]);
    }
}
