<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('events', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->nullable()->constrained()->nullOnDelete();
            $table->dateTime('event_date');
            $table->string('control')->default('medio'); // alto, medio, bajo
            $table->string('interferencia')->default('ninguna'); // ninguna, leve, severa
            $table->string('sintomas')->default('ninguno'); // ninguno, leve, moderado_severo
            $table->string('estres')->default('medio'); // bajo, medio, alto
            $table->boolean('porno')->default(false);
            $table->text('notas')->nullable();
            $table->integer('score')->default(100);
            $table->string('color')->default('green'); // green, yellow, red
            $table->text('explicacion')->nullable();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('events');
    }
};
